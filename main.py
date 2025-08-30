import os
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import call_function, available_functions
import argparse
import sys
from google import genai
from config import MAX_ITERS



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


if len(sys.argv) < 2:
    print("Error: Please provide a prompt")
    sys.exit(1)

prompt = sys.argv[1]

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="User prompt to send to the model")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

prompt = args.prompt


def main():
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    try:
        for i in range(20):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=available_functions,
                    system_instruction=system_prompt,
               ),
            )


            for cand in response.candidates or []:
                if cand.content:
                    messages.append(cand.content)
            

            if response.function_calls:
                function_responses = []
                for fc in response.function_calls:
                    result_content = call_function(fc, verbose=args.verbose)
                    function_responses.extend(result_content.parts)
                messages.append(types.Content(role="user", parts=function_responses))
                continue
        
             

            if response.text:
                print("Final response:")
                print(response.text)
                break
            break

    except Exception as e:
        print(f"Error: {e}")
            

    if args.verbose:
        print(f"User prompt: {prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)




if __name__ == "__main__":
    main()




