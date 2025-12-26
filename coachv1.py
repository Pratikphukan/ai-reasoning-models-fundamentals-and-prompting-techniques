import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

token = os.environ['OPENAI_API_KEY']

if not token:
    raise SystemExit("Error: Missing API key. Set OPEN_API_KEY.")

client = OpenAI(api_key=token)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": (
                    "You are an AI Personal Coach. "
                    "Provide clear, personalized, practical advice. "
                    "Respond concisely with 3-5 concrete steps."
                ),
            },
            {
                "role": "user",
                "content": "Provide steps I can take to reduce stress during the work week."
            }
        ],
    )

    print("\n--- AI Personal Coach Response ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"[Error] API call failed: {e}")