import os

print("[START]")

total_score = 0

try:
    import requests
except Exception as e:
    print("Import error:", e)
    exit(0)

try:
    from openai import OpenAI

    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL"),
        api_key=os.environ.get("API_KEY"),
    )
except Exception as e:
    print("LLM setup failed:", e)
    client = None

BASE_URL = "https://Mahakchoudhari-support-ticket-env.hf.space"



def safe_post(url, **kwargs):
    try:
        res = requests.post(url, timeout=10, **kwargs)
        return res.json()
    except Exception as e:
        print(f"[ERROR] {url} ->", e)
        return {}



def ask_llm(prompt, fallback=""):
    if client is None:
        return fallback

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print("LLM error:", e)
        return fallback


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
                    f"Classify this support ticket into one word (billing, technical, refund): {ticket}",
                    fallback="billing"
                )
                action = {"type": "classify", "content": result.lower()}

            elif step_num == 1:
                result = ask_llm(
                    f"What action should be taken? Choose one word (refund, troubleshoot, escalate): {ticket}",
                    fallback="refund"
                )
                action = {"type": "act", "content": result.lower()}

            else:
                result = ask_llm(
                    f"Write a short helpful response including apology and resolution for: {ticket}",
                    fallback="sorry we will help and resolve your issue with refund"
                )
                action = {"type": "respond", "content": result}

            data = safe_post(f"{BASE_URL}/step", json=action)

            obs = data.get("observation", {})
            reward = data.get("reward", 0)
            done = data.get("done", True)

            print("[STEP]", action, reward)

            step_num += 1

            if step_num > 5:
                break

            if done:
                total_score += reward

except Exception as e:
    print("[FATAL ERROR]", e)

print("[END] total_score:", total_score)

exit(0)