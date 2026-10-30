
import argparse
import os

# Keep these imports
from call_function import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is missing from environment variables."
    )

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Enable verbose output"
)
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

total_prompt_tokens = 0
total_response_tokens = 0
MAX_ITERATIONS = 20

# AGENT LOOP
for _ in range(MAX_ITERATIONS):

    # Ask the LLM
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    # Track token usage
    if response.usage:
        total_prompt_tokens += response.usage.prompt_tokens
        total_response_tokens += response.usage.completion_tokens
    message = response.choices[0].message
    messages.append(message.model_dump(exclude_none=True))

    # Check if the assistant wants to call tools
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(
                tool_call,
                verbose=args.verbose,
            )
            if not result_message.get("content"):
                raise Exception("Function call returned empty content")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
        continue
    print("AI Response:", message.content)
    break

else:
    print("Maximum agent iterations reached.")
if args.verbose:
    print(f"Total prompt tokens: {total_prompt_tokens}")
    print(f"Total response tokens: {total_response_tokens}")
