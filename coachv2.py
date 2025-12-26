import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

token = os.environ['OPENAI_API_KEY']

if not token:
    raise SystemExit("Error: Missing API key. Set OPEN_API_KEY.")

client = OpenAI(api_key=token)

def model_router(goal: str, quality: str):
    goal_text = goal.lower()
    wants_accuracy = quality.lower().startswith("a")
    complex_signals = any(keyword in goal_text for keyword in ["plan", "strategy", "trade-off", "analyze", "debug", "evaluate"])

    if wants_accuracy or complex_signals:
        return "o4-mini"
    else:
        return "gpt-4o-mini"
    

user_goal = input("\nWhat’s your goal or challenge? > ").strip()
if not user_goal:
    raise ValueError("No goal provided.")
    
# Ask for quality preference
quality = input("Optimize for 'speed' or 'accuracy'? [speed]: ").strip() or "speed"

model_name = model_router(user_goal, quality)
print(f"\n--- Using model: {model_name} ---\n")

try:
    response = client.chat.completions.create(
        model=model_name,
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