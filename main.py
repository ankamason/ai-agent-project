import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    max_iterations = 20
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        if verbose:
            print(f"\n--- Iteration {iteration} ---")
        
        # Generate response from AI
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        # Add AI's response to conversation
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        # Check if AI wants to call functions
        if not response.function_calls:
            # No function calls - AI is done, print final response and exit
            print("Final response:")
            print(response.text)
            break
        
        # Handle function calls
        function_called = False
        for function_call_part in response.function_calls:
            function_called = True
            function_call_result = call_function(function_call_part, verbose)
            
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Add function result to conversation
            messages.append(function_call_result)
        
        # If we've hit max iterations, stop
        if iteration >= max_iterations:
            print(f"Reached maximum iterations ({max_iterations}). Stopping.")
            break


if __name__ == "__main__":
    main()
