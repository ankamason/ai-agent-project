import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Check if prompt was provided as command line argument
if len(sys.argv) < 2:
    print("Error: No prompt provided!")
    print("Usage: python main.py \"Your question here\"")
    print("Example: python main.py \"What is artificial intelligence?\"")
    exit(1)

# Get the prompt from command line arguments
user_prompt = sys.argv[1]

# Create a structured conversation with roles
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

print(f"User prompt: {user_prompt}")
print(f"Message structure: {len(messages)} message(s) in conversation")
print("-" * 50)

# Get the API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

# Verify API key was loaded
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    print("Make sure your .env file exists and contains the API key")
    exit(1)

# Create a Gemini client
client = genai.Client(api_key=api_key)

# Generate content using the Gemini model with structured conversation
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
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
