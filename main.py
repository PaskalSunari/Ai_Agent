import argparse
import json  # 1. Added for parsing tool arguments
import os
from tabnanny import verbose
from unittest import result
from call_function import available_functions, call_function  
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
  raise ValueError("OPENROUTER_API_KEY is missing from environment variables.")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    temperature=0,
    tools=available_functions,  # 2. Passed available tools to the LLM
)

if args.verbose:
  print(f"User prompt: {args.user_prompt}")
  print(f"Prompt tokens: {response.usage.prompt_tokens}")
  print(f"Response tokens: {response.usage.completion_tokens}")

# 3. Handle tool calls vs. regular content response
message = response.choices[0].message

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
else:
  print("AI Response:", message.content)