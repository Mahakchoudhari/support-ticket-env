import os
import json
import urllib.request
from openai import OpenAI

print("[START]")

total_score = 0  # ✅ fixed typo

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"],
)

BASE_URL = "https://Mahakchoudhari-support-ticket-env.hf.space"


def safe_post(url, data):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("[ERROR]", e)
        return {}


def ask_llm(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    print("[LLM CALLED]")
    return res.choices[0].message.content.strip()


try:
    for task_id in range(3):

        data = safe_post(f"{BASE_URL}/reset", {"task_id": task_id})
        ticket = data.get("observation", {}).get("ticket", "")

        result = ask_llm(
            f"Classify the support ticket into EXACTLY one word: billing OR technical OR refund.\nTicket: {ticket}"
        ).strip().lower()

        if result not in ["billing", "technical", "refund"]:
            result = "billing"

        data = safe_post(f"{BASE_URL}/step", {
            "type": "classify",
            "content": result
        })

        result = ask_llm(
            f"Choose the best action in EXACTLY one word: refund OR troubleshoot OR escalate.\nTicket: {ticket}"
        ).strip().lower()

        if result not in ["refund", "troubleshoot", "escalate"]:
            result = "refund"

        data = safe_post(f"{BASE_URL}/step", {
            "type": "act",
            "content": result
        })

        result = ask_llm(
            f"Write a short (1-2 sentence) polite response with apology and clear resolution.\nTicket: {ticket}"
        )

        data = safe_post(f"{BASE_URL}/step", {
            "type": "respond",
            "content": result
        })

        reward = data.get("reward", 0)

        total_score += reward

        print("[TASK DONE]", task_id, "Reward:", reward)

except Exception as e:
    print("[FATAL ERROR]", e)

print("[END] total_score:", total_score)