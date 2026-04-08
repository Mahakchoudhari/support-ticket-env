import os
import requests
from openai import OpenAI

print("[START]")

total_score = 0

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"],
)

BASE_URL = "https://Mahakchoudhari-support-ticket-env.hf.space"


def safe_post(url, **kwargs):
    try:
        res = requests.post(url, timeout=10, **kwargs)
        return res.json()
    except Exception as e:
        print(f"[ERROR] {url} ->", e)
        return {}


def ask_llm(prompt):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        print("[LLM CALLED]")  
        return res.choices[0].message.content.strip()
    except Exception as e:
        print("LLM ERROR:", e)
        raise e  # ❗ don't silently fail


try:
    for task_id in range(3):

        data = safe_post(f"{BASE_URL}/reset", json={"task_id": task_id})
        obs = data.get("observation", {})

        done = False
        step_num = 0

        while not done:

            ticket = obs.get("ticket", "")

            if step_num == 0:
                result = ask_llm(
                    f"Classify this support ticket into one word (billing, technical, refund): {ticket}"
                )
                action = {"type": "classify", "content": result.lower()}

            elif step_num == 1:
                result = ask_llm(
                    f"What action should be taken? Choose one word (refund, troubleshoot, escalate): {ticket}"
                )
                action = {"type": "act", "content": result.lower()}

            else:
                result = ask_llm(
                    f"Write a short helpful response including apology and resolution for: {ticket}"
                )
                action = {"type": "respond", "content": result}

            data = safe_post(f"{BASE_URL}/step", json=action)

            obs = data.get("observation", {})
            reward = data.get("reward", 0)
            done = data.get("done", True)

            print("[STEP]", action, "Reward:", reward)

            step_num += 1

            if done:
                total_score += reward

            if step_num > 5:
                break

except Exception as e:
    print("[FATAL ERROR]", e)

print("[END] total_score:", total_score)