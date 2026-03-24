import os
import argparse
from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(20):
        if generate_response(client, messages, args):
            return
    exit(1)

def generate_response(client, messages, args):
    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )

    if res.candidates:
        for candidate in res.candidates:
            messages.append(candidate)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if res.usage_metadata is not None:
            print(f"Prompt tokens:{res.usage_metadata.prompt_token_count}")
            print(f"Response tokens:{res.usage_metadata.candidates_token_count}")
        else:
            raise RuntimeError("Usage metadata is None")
    rslt = ''
    func_rslt = []
    if res.function_calls:
        for call in res.function_calls:
            # print(f"Calling function: {call.name}({call.args})")
            func_call_rslt = call_function(call, call.args)
            if not func_call_rslt.parts:
                raise Exception("Response is an empty list")
            elif not func_call_rslt.parts[0].function_response:
                raise Exception("Function response is none")
            elif not func_call_rslt.parts[0].function_response.response:
                raise Exception("Response is none")
            else:
                func_rslt.append(func_call_rslt.parts[0])
                messages.append(types.Content(role="user", parts=func_rslt))
                if args.verbose:
                    print(f"-> {func_call_rslt.parts[0].function_response.response}")
                    return None
    else:
        print(f"Response: {res.text}")
        return res.text

if __name__ == "__main__":
    main()
