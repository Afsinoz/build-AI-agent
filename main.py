import os 
from dotenv import load_dotenv
import sys
from google.genai import Client, types
from functions.get_files_info import  schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_functions import call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Prompt is not provided!")
    sys.exit(1)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents 
- Execute Python files with optimal arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

You can run the functions without the arguments. 
"""

avaible_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file
    ]
)


user_prompt = sys.argv[1]

messages = []

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

for i in range(20):
    try:
        response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                                  contents=messages,
                                                  config=types.GenerateContentConfig(tools=[avaible_functions],
                                                  system_instruction=system_prompt))

#        if response.candidates:
#            messages.append(response.candidates[0].content) #type:ignore
        if response.candidates:
            for cand in response.candidates:
                messages.append(cand.content)
#                print("This is Candidate response START --------\n")
#                print(cand.content)
#                print("\n")
#                print("This is Candidate response END --------\n")

        if response.function_calls:
            for function_call in response.function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_return = call_function(function_call, verbose=("--verbose" in sys.argv))
#                print("------- FUNCTION RESULT START ------\n")
#                print(function_return.parts[0])
#                print("\n")
#                print("------- FUNCTION RESULT END ------\n")
                try:
                    out = function_return.parts[0].function_response.response #type:ignore
                except Exception:
                    raise RuntimeError("Missing function_response.response in call_function result")
                messages.append(
                    types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(name=function_call.name, response=out))])
                )
                #print("------- Messages Start-------\n")
                #print(messages)
                #print("------- Messages End-------\n")
        else:
            has_text = bool(response.text and response.text.strip())
            if has_text:
                print(f"{response.text}")
                break

    except Exception as e:
        print(f"Error: {e}")













#if "--verbose" in sys.argv:
#    print(f"User prompt: {user_prompt}")
#
#    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # type:ignore
#
#    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # type:ignore
#
#
#
#if response.function_calls:
#    for function_call in response.function_calls:
#        print(f"Calling function: {function_call.name}({function_call.args})")
#        function_return = call_function(function_call, verbose=("--verbose" in sys.argv))
#        try:
#            out = function_return.parts[0].function_response.response #type:ignore
#        except Exception:
#            raise RuntimeError("Missing function_response.response in call_function result")
#
#        if "--verbose" in sys.argv:
#            print(f"-> {out}")
#
#else:
#    print(response.text)
#


