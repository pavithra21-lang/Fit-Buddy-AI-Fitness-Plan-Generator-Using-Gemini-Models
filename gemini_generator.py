import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_workout_gemini(user_input: dict) -> str:
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of "{user_input['goal']}", and prefers **{user_input['intensity']}** intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    # Retry loop with backoff for handling 503 traffic spikes
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < 3:
                time.sleep(3 * (attempt + 1))  # Wait 3s, then 6s, then 9s
                continue
            return f"Error: {str(e)}"