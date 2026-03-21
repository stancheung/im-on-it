import os
import argparse
from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
prompt = args.user_prompt

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

res = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0,
    ),
)

if args.verbose:
    print(f"User prompt: {prompt}")
    if res.usage_metadata is not None:
        print(f"Prompt tokens:{res.usage_metadata.prompt_token_count}")
        print(f"Response tokens:{res.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Usage metadata is None")

rslt = ''
if res.function_calls:
    for call in res.function_calls:
        # print(f"Calling function: {call.name}({call.args})")
        func_call_rslt = call_function(call.name, call.args)
        if func_call_rslt.parts == None:
            raise Exception("Response is an empty list")
else:
    print(f"Response: {res.text}")
